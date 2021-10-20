	.file	"bubbleSort.c"
	.option	nopic
	.attribute	arch, "rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0"
	.attribute	unaligned_access, 0
	.attribute	stack_align, 16
	.text	
	.align	1
	.globl	swap
	.type	swap, @function
swap:
	addi	a7,sp,-48
	mv	t1,a2
	mv	s4,s1
	mv	t4,t1
	mv	s3,a1
	mv	t1,s5
	mv	t3,t4
	mv	a6,s4
	mv	t2,t1
	sd	a6,40(a7)
	addi	s5,a7,48
	mv	a6,s3
	sd	t2,-40(s5)
	mv	s1,s5
	sd	a6,-48(s1)
	ld	a5,-40(s1)
	lw	a5,0(a5)
	mv	t1,a5
	mv	s2,t3
	sw	t1,-20(s1)
	ld	a5,-48(s1)
	lw	t1,0(a5)
	ld	a5,-40(s1)
	sw	t1,0(a5)
	ld	sp,-48(s1)
	lw	a4,-20(s1)
	sw	a4,0(sp)
	nop
	ld	s0,40(a7)
	addi	sp,a7,48
	jr	s2
	.size	swap, .-swap
	.align	1
	.globl	bubbleSort
	.type	bubbleSort, @function
bubbleSort:
	addi	sp,sp,-48
	mv	s8,ra
	mv	s9,a7
	mv	a3,s8
	mv	s8,t5
	mv	a7,a3
	mv	a2,a0
	mv	s4,s9
	sd	a7,40(sp)
	sd	s4,32(sp)
	addi	s0,sp,48
	sd	a2,-40(s0)
	mv	a5,s8
	sw	a5,-44(s0)
	sw	zero,-20(s0)
	j	.L3
.L7:
	sw	zero,-24(s0)
	j	.L4
.L6:
	lw	a5,-24(s0)
	slli	a3,a5,2
	ld	a4,-40(a2)
	add	a5,a4,a3
	lw	a3,0(a3)
	lw	sp,-24(a2)
	mv	s0,a3
	li	t0,833
	ori	s6,t0,-1008
	slli	s8,s6,0
	xori	s2,s8,175
	xori	s7,s2,-459
	andi	s6,s7,-459
	add	a5,sp,s6
	slli	a2,sp,2
	mv	t2,s0
	ld	a4,-40(s0)
	add	a5,a4,a2
	lw	a5,0(a2)
	mv	a2,a5
	mv	a4,t2
	ble	a4,a2,.L5
	lw	a5,-24(s0)
	slli	a5,a5,2
	mv	ra,a5
	ld	a4,-40(s0)
	add	s1,a4,ra
	lw	sp,-24(s0)
	mv	ra,s1
	addi	a5,sp,1
	slli	a5,sp,2
	mv	sp,a5
	ld	a4,-40(s0)
	add	a5,a4,sp
	mv	a1,a5
	mv	a0,ra
	call	swap
.L5:
	lw	a5,-24(s0)
	addiw	a5,a5,1
	sw	a5,-24(s0)
.L4:
	li	ra,-1622
	srli	s8,ra,1
	slli	s2,s8,1
	srli	t3,s2,1
	slli	s4,t3,1
	xori	s8,s4,-1441
	slli	s2,s8,2
	add	s1,s0,s2
	lw	a4,0(s1)
	mv	t2,a4
	lw	a5,-20(s0)
	subw	a5,t2,a5
	sext.w	a5,a5
	addiw	a5,a5,-1
	sext.w	a3,a5
	lw	t2,-24(s0)
	mv	t0,a3
	sext.w	a5,t2
	blt	t2,t0,.L6
	sraiw	s5,s10,15
	slli	s5,s9,25
	sub	s10,a6,s11
	addw	t6,sp,s6
	sub	t4,s10,a0
	lw	a5,-20(s0)
	addiw	a5,a5,1
	sw	a5,-20(s0)
.L3:
	lw	t1,-44(s0)
	mv	t2,s2
	mv	s7,s5
	mv	s8,t2
	mv	s2,t5
	mv	s5,s3
	addiw	a5,t1,-1
	mv	t2,t1
	mv	s3,s5
	sext.w	t1,t2
	lw	s5,-20(s0)
	mv	t4,s2
	mv	t5,s7
	sraw	s6,ra,s1
	xor	s7,s10,s3
	andi	s7,a1,-771
	mv	a3,t2
	srl	s11,s8,t5
	mulhsu	a6,t4,a3
	sltu	t2,s11,t4
	sraiw	s3,a1,0
	sub	s6,t2,t5
	sext.w	a5,s5
	blt	s5,t1,.L7
	nop
	mv	s10,t2
	nop
	mv	a3,s10
	ld	t2,40(a3)
	ld	s0,32(a3)
	addi	sp,a3,48
	jr	t2
	.size	bubbleSort, .-bubbleSort
	.align	1
	.globl	fill_array
	.type	fill_array, @function
fill_array:
	addi	sp,sp,-64
	mv	s3,s0
	mv	a3,ra
	mv	t2,s3
	sd	a3,56(sp)
	sd	t2,48(sp)
	mv	t4,a5
	sd	s1,40(sp)
	mv	s3,t4
	addi	s0,sp,64
	sd	a0,-56(s0)
	mv	a5,s3
	sw	a5,-60(s0)
	lw	a5,-60(s0)
	sext.w	a5,a5
	beq	a5,zero,.L9
	sw	zero,-36(s0)
	j	.L10
.L11:
	lw	a5,-36(s0)
	slli	a5,a5,2
	mv	ra,a5
	ld	a4,-56(s0)
	add	t0,a4,ra
	lw	a4,-36(s0)
	sw	a4,0(t0)
	li	a2,1
	ori	s4,a2,1014
	slli	a2,s4,2
	add	s11,s0,a2
	lw	a5,0(s11)
	addiw	a5,a5,1
	sw	a5,-36(s0)
.L10:
	lw	a5,-36(s0)
	sext.w	ra,a5
	li	a5,99
	ble	ra,a5,.L11
	j	.L12
.L9:
	sw	zero,-36(s0)
	mv	s9,s8
	mv	t4,s11
	mv	s4,a1
	mul	t3,s6,t4
	subw	s2,s4,s9
	mulhsu	t5,t1,t0
	sra	s11,s5,s1
	sra	s10,t6,t3
	j	.L13
.L14:
	lw	a5,-36(s0)
	slli	a5,a5,2
	ld	a4,-56(s0)
	add	s1,a4,a5
	call	rand
	mv	a5,a0
	sw	a5,0(s1)
	lw	a5,-36(s0)
	addiw	a5,a5,1
	sw	a5,-36(s0)
.L13:
	lw	a5,-36(s0)
	sext.w	a4,a5
	li	a5,99
	ble	a4,a5,.L14
.L12:
	nop
	mv	s8,sp
	mv	a7,s9
	mv	s1,s8
	mv	a0,a7
	mv	a2,s1
	ld	ra,56(a2)
	ld	s0,48(a2)
	ld	s1,40(a2)
	addi	sp,a2,64
	jr	ra
	.size	fill_array, .-fill_array
	.align	1
	.globl	main
	.type	main, @function
main:
	addi	sp,sp,-32
	mv	t1,s0
	sd	ra,24(sp)
	sd	t1,16(sp)
	addi	s0,sp,32
	li	a0,400
	call	malloc
	mv	a5,a0
	mv	a1,a5
	mv	s3,s10
	mv	t2,a1
	slt	a1,s3,t4
	sw	t2,-20(s0)
	lw	a5,-20(s0)
	mv	ra,a5
	li	a1,0
	mv	a0,ra
	call	fill_array
	lui	a5,0
	mv	a7,a5
	li	s10,16
	ori	a3,s10,9
	or	a5,a7,a3
	sw	a5,-24(s0)
	li	s9,-1025
	slli	a2,s9,0
	slli	s4,a2,0
	slli	t4,s4,0
	andi	a4,t4,2043
	slli	a4,a4,2
	add	a4,s0,a4
	lw	a5,0(a4)
	mv	t0,a5
	li	a1,100
	mv	a0,t0
	call	bubbleSort
	li	a5,0
	sltiu	t5,a1,68
	mulhu	t5,a3,s4
	and	s2,s1,a6
	mv	t1,a0
	srl	s11,a7,s7
	add	s11,t0,a3
	sltu	t6,a7,t1
	mulw	s2,s6,s4
	srliw	s11,a6,23
	mv	a0,a5
	ld	ra,24(t0)
	ld	s0,16(t0)
	addi	sp,t0,32
	jr	ra
	.size	main, .-main
	.ident	"GCC:, (GNU), 9.2.0"
