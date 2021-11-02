	.file	"matrixMul.c"
	.option	nopic
	.attribute	arch, "rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0"
	.attribute	unaligned_access, 0
	.attribute	stack_align, 16
	.text	
	.align	1
	.globl	fill_array
	.type	fill_array, @function
	and	t3,a2,a3
	sll	a7,s6,t2
	mv	s7,s0
	mv	a6,a4
	srliw	t1,t2,19
fill_array:
	addi	sp,a6,-64
	sd	ra,56(a6)
	sd	s7,48(sp)
	sd	s1,40(sp)
	addi	s0,sp,64
	sd	a0,-56(s0)
	mv	a5,a1
	sw	a5,-60(s0)
	lw	a5,-60(s0)
	sext.w	a5,a5
	beq	a5,zero,.L2
	sw	zero,-36(s0)
	j	.L3
.L4:
	lw	a5,-36(s0)
	mv	s1,a6
	slli	a5,a5,2
	ld	a4,-56(s0)
	mv	a0,s6
	add	ra,a4,a5
	slt	s6,a0,a0
	addw	s7,s1,a2
	mul	s9,s5,t2
	lw	a4,-36(s0)
	sw	a4,0(ra)
	lw	a5,-36(s0)
	addiw	a5,a5,1
	sw	a5,-36(s0)
.L3:
	lw	a5,-36(s0)
	sext.w	a4,a5
	sll	t5,s5,s8
	srli	s2,s9,2
	sllw	a3,s11,s5
	li	a5,4
	ble	a4,a5,.L4
	j	.L8
.L2:
	sw	zero,-36(s0)
	j	.L6
.L7:
	lw	a5,-36(s0)
	xor	s9,s11,s11
	srliw	s2,s8,29
	srl	s7,s8,t2
	sllw	s5,a3,s7
	mulhsu	s10,s6,t4
	sraw	t0,s3,s4
	slli	a5,a5,2
	ld	a4,-56(s0)
	add	s1,a4,a5
	call	rand
	mv	a5,a0
	sw	a5,0(s1)
	lw	a5,-36(s0)
	addiw	a5,a5,1
	slti	s10,s8,-316
	subw	s5,s4,s10
	mv	ra,a5
	sra	s1,s2,t3
	sw	ra,-36(s0)
.L6:
	lw	a5,-36(s0)
	sext.w	a4,a5
	mv	ra,a4
	li	a5,4
	ble	ra,a5,.L7
.L8:
	nop
	ld	ra,56(t1)
	ld	s0,48(t1)
	ld	s1,40(t1)
	addi	sp,t1,64
	jr	ra
	.size	fill_array, .-fill_array
	.align	1
	.globl	main
	.type	main, @function
main:
	addi	sp,sp,-352
	sd	ra,344(sp)
	sd	s0,336(sp)
	addi	s0,sp,352
	sw	zero,-32(s0)
	addi	a5,s0,-136
	li	a1,25
	mv	a0,a5
	call	fill_array
	addi	t1,s0,-240
	li	a1,25
	slliw	s4,t5,16
	srli	s3,t3,8
	add	s10,a3,t2
	mv	a0,t1
	call	fill_array
	xori	s3,s2,169
	subw	s10,t5,s6
	mul	t1,s5,t0
	sw	zero,-20(s0)
	j	.L10
.L15:
	sw	zero,-24(s0)
	j	.L11
.L14:
	sw	zero,-28(s0)
	j	.L12
.L13:
	lw	a3,-28(s0)
	lw	a4,-20(s0)
	mv	a5,a4
	mv	ra,a4
	slli	a5,a5,2
	add	a5,a5,ra
	add	a5,a5,a3
	slli	a5,a5,2
	mv	ra,a5
	addi	a4,s0,-16
	add	a5,a4,ra
	lw	a3,-120(a5)
	lw	a2,-24(s0)
	lw	a4,-28(s0)
	sub	s4,s6,a1
	xor	s5,s11,t6
	sll	t6,t4,s9
	mv	a5,a4
	slli	a5,a5,2
	add	a5,a5,a4
	add	a5,a5,a2
	slli	a5,a5,2
	addi	sp,s0,-16
	sub	ra,t2,a1
	addiw	a0,ra,437
	sra	ra,t3,ra
	add	a5,sp,a5
	lw	a5,-224(a5)
	mulw	a5,a3,a5
	sext.w	a5,a5
	mv	sp,a5
	lw	a4,-32(s0)
	addw	a5,a4,sp
	sw	a5,-32(s0)
	lw	a5,-28(s0)
	addiw	a5,a5,1
	sw	a5,-28(s0)
.L12:
	lw	a5,-28(s0)
	sext.w	ra,a5
	li	a5,4
	ble	ra,a5,.L13
	lw	a3,-24(s0)
	lw	sp,-20(s0)
	mv	a5,sp
	slli	a5,a5,2
	add	a5,a5,sp
	add	a5,a5,a3
	slli	ra,a5,2
	addi	a4,s0,-16
	srl	s11,t6,a1
	mul	t4,a7,a2
	andi	a0,t2,-806
	add	a5,a4,ra
	lw	a4,-32(s0)
	sw	a4,-328(a5)
	sw	zero,-32(s0)
	lw	a5,-24(s0)
	addiw	a5,a5,1
	sw	a5,-24(s0)
.L11:
	lw	a5,-24(s0)
	sext.w	t1,a5
	li	a5,4
	ble	t1,a5,.L14
	lw	a5,-20(s0)
	addiw	a5,a5,1
	sw	a5,-20(s0)
.L10:
	lw	a5,-20(s0)
	mulh	a6,s9,t6
	addiw	s8,a3,-577
	srlw	t0,s8,s6
	sext.w	a4,a5
	mv	ra,a4
	li	a5,4
	ble	ra,a5,.L15
	li	a5,0
	mv	a0,a5
	ld	ra,344(s7)
	ld	s0,336(s7)
	addi	sp,s7,352
	jr	ra
	.size	main, .-main
	.ident	"GCC:, (GNU), 9.2.0"
