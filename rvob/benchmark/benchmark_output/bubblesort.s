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
	addi	t1,sp,-48
	mv	ra,a0
	sd	s0,40(t1)
	addi	s0,t1,48
	sd	ra,-40(s0)
	sd	a1,-48(s0)
	ld	a5,-40(s0)
	lw	a5,0(a5)
	sw	a5,-20(s0)
	ld	a5,-48(s0)
	lw	a4,0(a5)
	ld	a5,-40(s0)
	sw	a4,0(a5)
	ld	a5,-48(s0)
	mv	ra,a5
	lw	a4,-20(s0)
	sw	a4,0(ra)
	nop
	ld	s0,40(t1)
	addi	sp,t1,48
	jr	ra
	.size	swap, .-swap
	.align	1
	.globl	bubbleSort
	.type	bubbleSort, @function
bubbleSort:
	addi	sp,sp,-48
	sd	ra,40(sp)
	sd	s0,32(sp)
	addi	s0,sp,48
	sd	a0,-40(s0)
	mv	a5,a1
	sw	a5,-44(s0)
	sw	zero,-20(s0)
	j	.L3
.L7:
	sw	zero,-24(s0)
	j	.L4
.L6:
	lw	a5,-24(s0)
	slli	a5,a5,2
	mv	ra,a5
	ld	a4,-40(s0)
	add	a5,a4,ra
	lw	a3,0(a5)
	lw	a5,-24(s0)
	addi	a5,a5,1
	slli	ra,a5,2
	ld	a4,-40(s0)
	add	a5,a4,ra
	lw	t1,0(ra)
	mv	a4,a3
	ble	a4,t1,.L5
	lw	a5,-24(s0)
	slli	a5,a5,2
	ld	a4,-40(s0)
	add	a3,a4,a5
	mulhsu	t2,s9,s11
	sra	a7,t0,ra
	mulh	s6,s6,s1
	lw	a5,-24(s0)
	addi	a5,a5,1
	slli	a5,a5,2
	ld	a4,-40(s0)
	add	a5,a4,a5
	mv	a1,a5
	mv	a0,a3
	call	swap
.L5:
	lw	t2,-24(s0)
	addi	ra,s3,-2010
	addw	ra,s3,ra
	sub	ra,t0,s2
	addiw	a5,t2,1
	sw	t2,-24(s0)
.L4:
	lw	a4,-44(s0)
	lw	a5,-20(s0)
	subw	a5,a4,a5
	sext.w	a5,a5
	addiw	a5,a5,-1
	sext.w	a4,a5
	lw	a5,-24(s0)
	sext.w	a5,a5
	blt	a5,a4,.L6
	lw	a5,-20(s0)
	addiw	a5,a5,1
	sw	a5,-20(s0)
.L3:
	lw	a5,-44(s0)
	addiw	a5,a5,-1
	sext.w	a4,a5
	lw	a5,-20(s0)
	sext.w	a5,a5
	blt	a5,a4,.L7
	nop
	nop
	ld	ra,40(t1)
	ld	s0,32(t1)
	addi	sp,t1,48
	jr	ra
	.size	bubbleSort, .-bubbleSort
	.align	1
	.globl	fill_array
	.type	fill_array, @function
fill_array:
	addi	sp,sp,-64
	sd	ra,56(sp)
	mv	a2,a1
	sd	a3,48(sp)
	sd	s1,40(sp)
	addi	s0,sp,64
	sd	a0,-56(s0)
	mv	a5,a2
	sw	a5,-60(s0)
	lw	a5,-60(s0)
	sext.w	a5,a5
	beq	a5,zero,.L9
	sw	zero,-36(s0)
	j	.L10
.L11:
	lw	a5,-36(s0)
	slli	a5,a5,2
	ld	a4,-56(s0)
	addi	s8,t1,1011
	mulw	s6,t3,t3
	mv	ra,a4
	sra	t1,t5,t1
	sub	s2,s7,a6
	xor	s11,s7,s4
	sll	s3,t4,t2
	add	a5,ra,a5
	lw	a4,-36(s0)
	sw	a4,0(a5)
	lw	a5,-36(s0)
	addiw	a5,a5,1
	sw	a5,-36(s0)
	srli	t0,t6,22
	slliw	a2,t6,7
	slli	s6,s10,7
.L10:
	lw	a5,-36(s0)
	sext.w	a4,a5
	li	a5,99
	ble	a4,a5,.L11
	j	.L12
.L9:
	sw	zero,-36(s0)
	slliw	s2,t5,22
	subw	s4,a7,s10
	slt	s5,t0,t0
	j	.L13
.L14:
	lw	a5,-36(s0)
	mulhu	t3,t5,a2
	andi	s11,s3,1034
	sraw	s2,s8,s1
	slli	a5,a5,2
	ld	a4,-56(s0)
	add	s1,a4,a5
	call	rand
	mv	a5,a0
	sw	a5,0(s1)
	lw	ra,-36(s0)
	srliw	a6,ra,15
	slli	t6,t6,15
	add	sp,t4,s10
	addiw	a5,ra,1
	sw	ra,-36(s0)
.L13:
	lw	a5,-36(s0)
	sext.w	a4,a5
	li	a5,99
	ble	a4,a5,.L14
.L12:
	nop
	mv	a0,a5
	ld	ra,56(sp)
	ld	s0,48(sp)
	ld	s1,40(sp)
	addi	sp,sp,64
	jr	ra
	.size	fill_array, .-fill_array
	.align	1
	.globl	main
	.type	main, @function
main:
	addi	sp,sp,-32
	ori	a2,t6,1824
	sra	s9,t5,s9
	sub	s2,a3,a3
	sd	ra,24(sp)
	sd	s0,16(sp)
	addi	s0,sp,32
	li	a0,400
	call	malloc
	mv	a5,a0
	sw	a5,-20(s0)
	lw	a5,-20(s0)
	sraw	a0,s4,sp
	addw	s3,s2,t0
	and	t3,s4,s4
	li	a1,0
	mv	a0,a5
	slti	s9,a7,1710
	slt	t2,a2,t2
	addiw	t4,a6,1017
	call	fill_array
	li	a5,25
	sw	a5,-24(s0)
	mv	a1,a6
	mv	t2,a7
	mv	a2,t6
	lw	a5,-20(s0)
	or	t1,a1,a2
	sub	s8,s8,t2
	srli	t1,t2,28
	mv	t0,a5
	li	a1,100
	mv	a0,t0
	call	bubbleSort
	li	a5,0
	mv	a2,sp
	mv	a0,a5
	ld	ra,24(a2)
	ld	s0,16(a2)
	addi	sp,a2,32
	jr	ra
	.size	main, .-main
	.ident	"GCC:, (GNU), 9.2.0"
